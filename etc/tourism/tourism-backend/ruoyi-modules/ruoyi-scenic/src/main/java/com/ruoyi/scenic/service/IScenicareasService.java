package com.ruoyi.scenic.service;

import java.util.List;
import com.ruoyi.scenic.domain.Scenicareas;

/**
 * 景区信息Service接口
 * 
 * @author ningf
 * @date 2024-07-17
 */
public interface IScenicareasService 
{
    /**
     * 查询景区信息
     * 
     * @param id 景区信息主键
     * @return 景区信息
     */
    public Scenicareas selectScenicareasById(Long id);

    /**
     * 查询景区信息列表
     * 
     * @param scenicareas 景区信息
     * @return 景区信息集合
     */
    public List<Scenicareas> selectScenicareasList(Scenicareas scenicareas);

    /**
     * 新增景区信息
     * 
     * @param scenicareas 景区信息
     * @return 结果
     */
    public int insertScenicareas(Scenicareas scenicareas);

    /**
     * 修改景区信息
     * 
     * @param scenicareas 景区信息
     * @return 结果
     */
    public int updateScenicareas(Scenicareas scenicareas);

    /**
     * 批量删除景区信息
     * 
     * @param ids 需要删除的景区信息主键集合
     * @return 结果
     */
    public int deleteScenicareasByIds(Long[] ids);

    /**
     * 删除景区信息信息
     * 
     * @param id 景区信息主键
     * @return 结果
     */
    public int deleteScenicareasById(Long id);
}
